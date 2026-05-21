const EN_AUDIO_BASE =
  "https://clawdassistant85-netizen.github.io/openclaw-podcast-audio/audio";
const EN_ARCHIVE_BASE =
  "https://github.com/clawdassistant85-netizen/openclaw-podcast-media-en/releases/download";
const EN_ARCHIVE_CUTOFF_EPISODE = 32;

const RELEASE_REPOS = {
  es: "clawdassistant85-netizen/openclaw-podcast-media-es",
  de: "clawdassistant85-netizen/openclaw-podcast-media-de",
  pt: "clawdassistant85-netizen/openclaw-podcast-media-pt",
  hi: "clawdassistant85-netizen/openclaw-podcast-media-hi",
};

const FORWARDED_REQUEST_HEADERS = [
  "range",
  "if-none-match",
  "if-modified-since",
  "if-range",
];

const PASSTHROUGH_RESPONSE_HEADERS = [
  "accept-ranges",
  "cache-control",
  "content-length",
  "content-range",
  "etag",
  "expires",
  "last-modified",
  "date",
];

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

function badRequest(message, status = 400) {
  return jsonResponse({ error: message }, status);
}

function buildUpstreamUrl(lang, filename) {
  if (!/^episode_\d{3}\.mp3$/.test(filename)) {
    return null;
  }

  if (lang === "en") {
    const episode = filename.match(/^episode_(\d{3})\.mp3$/)?.[1];
    if (!episode) {
      return null;
    }
    const epNum = Number(episode);
    if (Number.isFinite(epNum) && epNum <= EN_ARCHIVE_CUTOFF_EPISODE) {
      return `${EN_ARCHIVE_BASE}/ep${episode}/${filename}`;
    }
    return `${EN_AUDIO_BASE}/${filename}`;
  }

  const repo = RELEASE_REPOS[lang];
  if (!repo) {
    return null;
  }

  const episode = filename.match(/^episode_(\d{3})\.mp3$/)?.[1];
  if (!episode) {
    return null;
  }

  return `https://github.com/${repo}/releases/download/ep${episode}/${filename}`;
}

function proxyResponseHeaders(upstreamHeaders, filename) {
  const headers = new Headers();

  for (const name of PASSTHROUGH_RESPONSE_HEADERS) {
    const value = upstreamHeaders.get(name);
    if (value) {
      headers.set(name, value);
    }
  }

  headers.set("content-type", "audio/mpeg");
  headers.set("content-disposition", `inline; filename="${filename}"`);
  headers.set("access-control-allow-origin", "*");
  headers.set("access-control-expose-headers", "Accept-Ranges, Content-Length, Content-Range, Content-Type, ETag, Last-Modified");
  headers.set("x-robots-tag", "noindex");
  return headers;
}

async function handleAudioRequest(request, lang, filename) {
  const upstreamUrl = buildUpstreamUrl(lang, filename);
  if (!upstreamUrl) {
    return badRequest("Unsupported audio path.", 404);
  }

  const upstreamHeaders = new Headers();
  for (const name of FORWARDED_REQUEST_HEADERS) {
    const value = request.headers.get(name);
    if (value) {
      upstreamHeaders.set(name, value);
    }
  }

  const upstream = await fetch(upstreamUrl, {
    method: request.method,
    headers: upstreamHeaders,
    redirect: "follow",
  });

  if (upstream.status >= 400) {
    const headers = proxyResponseHeaders(upstream.headers, filename);
    headers.set("content-type", "text/plain; charset=utf-8");
    headers.delete("content-disposition");
    return new Response(`Upstream audio fetch failed: ${upstream.status}`, {
      status: upstream.status,
      headers,
    });
  }

  const headers = proxyResponseHeaders(upstream.headers, filename);
  if (request.method === "HEAD") {
    return new Response(null, {
      status: upstream.status,
      headers,
    });
  }

  return new Response(upstream.body, {
    status: upstream.status,
    headers,
  });
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "access-control-allow-origin": "*",
          "access-control-allow-methods": "GET, HEAD, OPTIONS",
          "access-control-allow-headers": "Range, If-Range, If-None-Match, If-Modified-Since",
        },
      });
    }

    if (!["GET", "HEAD"].includes(request.method)) {
      return badRequest("Only GET and HEAD are supported.", 405);
    }

    if (url.pathname === "/" || url.pathname === "") {
      return jsonResponse({
        ok: true,
        service: "openclaw-audio-proxy",
        usage: "/audio/{lang}/episode_033.mp3",
        supportedLanguages: ["en", "es", "de", "pt", "hi"],
      });
    }

    const match = url.pathname.match(/^\/audio\/([a-z]{2})\/(episode_\d{3}\.mp3)$/);
    if (!match) {
      return badRequest("Expected /audio/{lang}/episode_XXX.mp3", 404);
    }

    const [, lang, filename] = match;
    return handleAudioRequest(request, lang, filename);
  },
};

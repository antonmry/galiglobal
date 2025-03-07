# HTML to Markdown Migration Plan

The goal is to migrate this blog from HTML to Markdown without breaking the links.

We are using this as a guide:

<script type="module">
  import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
  document.getElementById('content').innerHTML =
    marked.parse('# Marked in the browser\n\nRendered by **marked**.');
</script>
# Blog Post Conversion Guide

This guide provides instructions for converting all HTML blog posts to markdown format and updating the HTML files to load the markdown content.

## Overview

The conversion process involves two main steps:
1. Converting the HTML content to markdown format
2. Updating the HTML file to load the markdown content

## Templates

### Markdown Template

```markdown
# [Blog Post Title]

*[Publication Date]*

[Blog Post Content in Markdown Format]
```

### HTML Template

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>[Blog Post Title]</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="antonmry">
    <meta name="keywords" content="">
    <meta name="generator" content="JBake">

    <!-- Le styles -->
    <link href="../../css/bootstrap.min.css" rel="stylesheet">
    <link href="../../css/asciidoctor.css" rel="stylesheet">
    <link href="../../css/base.css" rel="stylesheet">
    <link href="../../css/prettify.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="../../js/html5shiv.min.js"></script>
    <![endif]-->

    <!-- Fav and touch icons -->
    <link rel="shortcut icon" href="../../favicon.ico">
  </head>
  <body>
    <div id="wrap">
      <div id="navbar-container"></div>
      <div class="container">
        <div id="content"></div>
      </div>
      <div id="push"></div>
    </div>

    <div id="footer-container"></div>

    <!-- Required scripts -->
    <script src="../../js/jquery-1.11.1.min.js"></script>
    <script src="../../js/bootstrap.min.js" defer></script>
    <script src="../../js/prettify.js" defer></script>

    <script type="module">
      import { marked } from '../../js/marked.esm.js';
      window.marked = marked;
    </script>

    <script>
      // Function to load HTML content
      async function loadContent(url, elementId) {
        try {
          const response = await fetch(url);
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          const html = await response.text();
          document.getElementById(elementId).innerHTML = html;
        } catch (error) {
          console.error(`Error loading ${url}:`, error);
        }
      }

      // Load all content when DOM is ready
      document.addEventListener('DOMContentLoaded', async () => {
        try {
          // Load components
          await loadContent('../../navbar.html', 'navbar-container');
          await loadContent('../../footer.html', 'footer-container');

          // Load markdown content
          const response = await fetch('[Markdown Filename]');
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
          const markdown = await response.text();
          document.getElementById('content').innerHTML = window.marked.parse(markdown);

          // Initialize prettify after content is loaded
          if (typeof prettyPrint === 'function') {
            prettyPrint();
          } else {
            console.error('prettyPrint function not available');
          }
        } catch (error) {
          console.error('Error loading content:', error);
          document.getElementById('content').innerHTML = 'Error loading content';
        }
      });
    </script>
  </body>
</html>
```

## Conversion Process

For each HTML blog post:

1. Extract the title, date, and content from the HTML file
2. Convert the HTML content to markdown format
3. Create a new markdown file with the same name as the HTML file but with a .md extension
4. Update the HTML file to load the markdown content

## Example

### Original HTML File: `blog/2025/20250204-monitoring-requests-with-minio.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>Monitoring MinIO requests with the OpenTelemetry Collector</title>
    <!-- ... -->
  </head>
  <body>
    <!-- ... -->
    <div class="page-header">
      <h1>Monitoring MinIO requests with the OpenTelemetry Collector</h1>
    </div>
    <p><em>04 February 2025</em></p>
    <p><!-- Blog content --></p>
    <!-- ... -->
  </body>
</html>
```

### New Markdown File: `blog/2025/20250204-monitoring-requests-with-minio.md`

```markdown
# Monitoring MinIO requests with the OpenTelemetry Collector

*04 February 2025*

I've been working on using Object Storage with Apache Flink to replace Kafka compacted topics...
```

### Updated HTML File: `blog/2025/20250204-monitoring-requests-with-minio.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8"/>
    <title>Monitoring MinIO requests with the OpenTelemetry Collector</title>
    <!-- ... -->
  </head>
  <body>
    <div id="wrap">
      <div id="navbar-container"></div>
      <div class="container">
        <div id="content"></div>
      </div>
      <div id="push"></div>
    </div>
    <div id="footer-container"></div>
    <!-- Scripts to load markdown content -->
    <!-- ... -->
  </body>
</html>
```

## Automation

To automate this process, you could use a script that:

1. Finds all HTML files in the blog folder
2. For each file, extracts the title, date, and content
3. Converts the content to markdown
4. Creates a new markdown file
5. Updates the HTML file to load the markdown content

## Implementation Steps

1. Create a markdown file for each HTML blog post
2. Update each HTML file to load its corresponding markdown file
3. Update all links in the navbar.html file to point to the HTML files (which now load markdown content)
4. Test the changes to ensure everything works correctly

## Notes

- Make sure to handle special characters and HTML entities correctly when converting to markdown
- Ensure that all links and images are properly referenced in the markdown files
- Test the changes thoroughly to ensure that all content is displayed correctly
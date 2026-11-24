import os
from flask import Flask, jsonify, render_template_string

application = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello from AWS Elastic Beanstalk!")

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Welcome to Elastic Beanstalk</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Instrument+Sans:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --ink: #10283a;
      --muted: #4a6275;
      --paper: #f2f6f3;
      --line: #c9d6d0;
      --green: #2f8f5b;
      --amber: #e8962e;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 48px 20px;
      color: var(--ink);
      background-color: var(--paper);
      background-image:
        linear-gradient(var(--line) 1px, transparent 1px),
        linear-gradient(90deg, var(--line) 1px, transparent 1px);
      background-size: 48px 48px;
      background-position: -1px -1px;
      font-family: "Instrument Sans", system-ui, sans-serif;
      line-height: 1.55;
    }
    main {
      width: 100%;
      max-width: 760px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: clamp(28px, 6vw, 56px);
    }
    h1 {
      margin: 0 0 16px;
      font-family: "Bricolage Grotesque", system-ui, sans-serif;
      font-weight: 700;
      font-size: clamp(2.3rem, 7vw, 4.2rem);
      line-height: 1.02;
      letter-spacing: -0.025em;
    }
    .lede {
      margin: 0;
      max-width: 52ch;
      font-size: 1.1rem;
      color: var(--muted);
    }
    .lede strong { color: var(--ink); font-weight: 500; }

    /* The one moment: a build travelling down the pipeline */
    .pipe {
      position: relative;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      margin: 56px 0 40px;
      padding: 0;
      list-style: none;
    }
    .pipe::before, .pipe::after {
      content: "";
      position: absolute;
      top: 13px;
      left: 16.666%;
      height: 4px;
      border-radius: 2px;
    }
    .pipe::before { right: 16.666%; background: var(--line); }
    .pipe::after {
      width: 66.666%;
      background: var(--green);
      transform-origin: left;
      transform: scaleX(0);
      animation: run 3.2s linear 0.4s forwards;
    }
    .pipe li { position: relative; z-index: 1; text-align: center; }
    .dot {
      display: block;
      width: 30px;
      height: 30px;
      margin: 0 auto 12px;
      border-radius: 50%;
      background: var(--paper);
      border: 3px solid var(--line);
      animation: on 0.2s forwards;
    }
    .pipe li:nth-child(1) .dot { animation-delay: 0.4s; }
    .pipe li:nth-child(2) .dot { animation-delay: 2s; }
    .pipe li:nth-child(3) .dot { animation-delay: 3.6s; }
    .pipe li:nth-child(3) .dot::after {
      content: "";
      display: block;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      opacity: 0;
      animation: ring 2s ease-out 3.8s infinite;
    }
    .pipe b { display: block; font-weight: 500; }
    .pipe span.sub { font-size: 0.85rem; color: var(--muted); }
    .live {
      opacity: 0;
      animation: fade 0.5s ease 3.6s forwards;
      color: var(--green);
    }

    dl {
      display: grid;
      grid-template-columns: max-content 1fr;
      gap: 10px 28px;
      margin: 0;
      padding: 20px 24px;
      border: 1px solid var(--line);
      border-left: 4px solid var(--amber);
      border-radius: 10px;
      background: #fff;
    }
    dt { color: var(--muted); }
    dd { margin: 0; font-weight: 500; overflow-wrap: anywhere; }
    a { color: var(--ink); text-underline-offset: 3px; }
    a:hover { color: var(--green); }
    a:focus-visible { outline: 3px solid var(--amber); outline-offset: 3px; border-radius: 2px; }

    @keyframes run { to { transform: scaleX(1); } }
    @keyframes on { to { background: var(--green); border-color: var(--green); } }
    @keyframes fade { to { opacity: 1; } }
    @keyframes ring {
      0% { box-shadow: 0 0 0 0 rgba(47, 143, 91, 0.45); opacity: 1; }
      100% { box-shadow: 0 0 0 18px rgba(47, 143, 91, 0); opacity: 1; }
    }
    @media (prefers-reduced-motion: reduce) {
      .pipe::after { animation: none; transform: scaleX(1); }
      .dot { animation: none; background: var(--green); border-color: var(--green); }
      .pipe li:nth-child(3) .dot::after { animation: none; }
      .live { animation: none; opacity: 1; }
    }
    @media (max-width: 480px) {
      dl { grid-template-columns: 1fr; gap: 2px; }
      dd { margin-bottom: 10px; }
    }
  </style>
</head>
<body>
  <main>
    <h1>Welcome to Elastic Beanstalk</h1>
    <p class="lede">
      This application was deployed using AWS CodeBuild and CodePipeline
      by <strong>Dhruv Rajput</strong>.
    </p>

    <ol class="pipe" aria-label="Deployment pipeline">
      <li><span class="dot"></span><b>Source</b><span class="sub">Code pushed</span></li>
      <li><span class="dot"></span><b>Build</b><span class="sub">CodeBuild</span></li>
      <li><span class="dot"></span><b>Deploy</b><span class="sub live">Live on Elastic Beanstalk</span></li>
    </ol>

    <dl>
      <dt>Message</dt><dd>{{ message }}</dd>
      <dt>Environment</dt><dd>{{ env }}</dd>
      <dt>Version</dt><dd>{{ version }}</dd>
      <dt>Platform</dt><dd>Python + Flask</dd>
      <dt>Health check</dt><dd><a href="/health">/health</a></dd>
    </dl>
  </main>
</body>
</html>
"""


@application.route("/")
def home():
    return render_template_string(
        PAGE, message=APP_MESSAGE, env=APP_ENV, version=APP_VERSION
    )


@application.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "environment": APP_ENV,
        "version": APP_VERSION
    })


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
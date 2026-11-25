import socket
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Docker + AWS ECR CI/CD Pipeline</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;700&family=Public+Sans:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --ink: #0b2540;
      --muted: #4a627a;
      --paper: #edf3fa;
      --line: #c3d3e4;
      --blue: #1d63ed;
      --orange: #e8862a;
      --green: #22a06b;
      --bw: clamp(44px, 10vw, 56px);
      --bh: calc(var(--bw) * 0.68);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 40px 16px;
      color: var(--ink);
      background-color: var(--paper);
      background-image: radial-gradient(var(--line) 1.5px, transparent 1.5px);
      background-size: 28px 28px;
      font-family: "Public Sans", system-ui, sans-serif;
      line-height: 1.55;
    }
    main {
      width: 100%;
      max-width: 780px;
      padding: clamp(24px, 6vw, 56px);
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 16px;
    }
    h1 {
      margin: 0 0 16px;
      font-family: "Familjen Grotesk", system-ui, sans-serif;
      font-weight: 700;
      font-size: clamp(2.1rem, 6.5vw, 3.8rem);
      line-height: 1.04;
      letter-spacing: -0.02em;
    }
    .lede { margin: 0; max-width: 54ch; font-size: 1.08rem; color: var(--muted); }
    .lede strong { color: var(--ink); font-weight: 500; }

    /* The one moment: layers pack into an image, ship to ECR, then run */
    .scene { position: relative; height: 140px; margin: 56px 0 22px; }
    .scene::after {
      content: "";
      position: absolute;
      left: 16.666%; right: 16.666%; bottom: -7px;
      border-top: 2px dashed var(--line);
    }
    .stack {
      position: absolute;
      left: 16.666%; bottom: 0;
      width: 30%; max-width: 130px;
      display: flex; flex-direction: column-reverse; gap: 3px;
      transform: translateX(-50%);
      transform-origin: bottom center;
      animation: pack 0.35s ease 2.4s forwards;
    }
    .layer {
      height: 24px;
      padding: 0 8px;
      display: flex; align-items: center;
      border-radius: 4px;
      color: #fff;
      font-size: clamp(0.58rem, 2.4vw, 0.75rem);
      white-space: nowrap; overflow: hidden;
      animation: layer 0.4s ease-out both;
    }
    .layer:nth-child(1) { background: #0f47bd; animation-delay: 0.3s; }
    .layer:nth-child(2) { background: #1d63ed; animation-delay: 0.75s; }
    .layer:nth-child(3) { background: #3f7ff2; animation-delay: 1.2s; }
    .layer:nth-child(4) { background: #3a6fc9; animation-delay: 1.65s; }

    .slot, .ghost, .pulse, .box {
      position: absolute; bottom: 0;
      width: var(--bw); height: var(--bh);
      margin-left: calc(var(--bw) / -2);
      border-radius: 4px;
    }
    .slot { border: 2px dashed var(--line); }
    .slot.ecr { left: 50%; }
    .slot.run { left: 83.333%; }

    .box, .ghost {
      background-color: var(--blue);
      background-image:
        repeating-linear-gradient(90deg, rgba(255,255,255,.22) 0 2px, transparent 2px 7px),
        linear-gradient(90deg, transparent 48%, rgba(0,0,0,.25) 48% 52%, transparent 52%);
    }
    .box { left: 16.666%; animation: travel 5s ease-in-out 2.4s both; }
    .ghost {
      left: 50%;
      background-color: var(--orange);
      opacity: 0;
      animation: show 0.4s ease 5.5s forwards;
    }
    .tag {
      position: absolute; left: 50%; bottom: calc(var(--bh) + 8px);
      transform: translateX(-50%);
      padding: 1px 10px;
      border-radius: 99px;
      background: var(--orange); color: #fff;
      font-size: 0.75rem; font-weight: 500;
      opacity: 0;
      animation: show 0.4s ease 5.7s forwards;
    }
    .pulse { left: 83.333%; animation: ring 2s ease-out 7.4s infinite; }

    .stations { display: grid; grid-template-columns: repeat(3, 1fr); margin: 0; padding: 0; list-style: none; text-align: center; }
    .stations b { display: block; font-weight: 500; }
    .stations span { font-size: 0.85rem; color: var(--muted); }
    .stations .live { color: var(--green); opacity: 0; animation: show 0.5s ease 7.4s forwards; }

    dl {
      display: grid; grid-template-columns: max-content 1fr; gap: 10px 28px;
      margin: 40px 0 0; padding: 20px 24px;
      background: #fff;
      border: 1px solid var(--line); border-left: 4px solid var(--orange); border-radius: 10px;
    }
    dt { color: var(--muted); }
    dd { margin: 0; font-weight: 500; overflow-wrap: anywhere; }
    a { color: var(--ink); text-underline-offset: 3px; }
    a:hover { color: var(--blue); }
    a:focus-visible { outline: 3px solid var(--orange); outline-offset: 3px; border-radius: 2px; }

    @keyframes layer { from { opacity: 0; transform: translateY(-16px); } to { opacity: 1; transform: none; } }
    @keyframes pack { to { opacity: 0; transform: translateX(-50%) scale(0.5); } }
    @keyframes show { to { opacity: 1; } }
    @keyframes travel {
      0%   { left: 16.666%; opacity: 0; background-color: var(--blue); }
      6%   { opacity: 1; }
      18%  { left: 16.666%; }
      40%  { left: 50%; }
      60%  { left: 50%; }
      85%  { left: 83.333%; background-color: var(--blue); }
      100% { left: 83.333%; opacity: 1; background-color: var(--green); }
    }
    @keyframes ring {
      from { box-shadow: 0 0 0 0 rgba(34, 160, 107, 0.5); }
      to   { box-shadow: 0 0 0 16px rgba(34, 160, 107, 0); }
    }
    @media (prefers-reduced-motion: reduce) {
      .stack { opacity: 0; animation: none; }
      .layer { animation: none; }
      .box { animation: none; left: 83.333%; background-color: var(--green); }
      .ghost, .tag, .stations .live { animation: none; opacity: 1; }
      .pulse { animation: none; }
    }
    @media (max-width: 480px) {
      dl { grid-template-columns: 1fr; gap: 2px; }
      dd { margin-bottom: 10px; }
    }
  </style>
</head>
<body>
  <main>
    <h1>Docker + AWS ECR CI/CD Pipeline</h1>
    <p class="lede">
      This application is running inside a Docker container, built by AWS CodeBuild
      and stored in Amazon ECR. Deployed by <strong>Dhruv Rajput</strong>.
    </p>

    <div class="scene" aria-hidden="true">
      <div class="stack">
        <div class="layer">Base image</div>
        <div class="layer">Dependencies</div>
        <div class="layer">App code</div>
        <div class="layer">Start command</div>
      </div>
      <div class="slot ecr"></div>
      <div class="slot run"></div>
      <div class="ghost"></div>
      <div class="tag">latest</div>
      <div class="pulse"></div>
      <div class="box"></div>
    </div>

    <ol class="stations" aria-label="Pipeline stages">
      <li><b>CodeBuild</b><span>Builds the image</span></li>
      <li><b>Amazon ECR</b><span>Stores the image</span></li>
      <li><b>Container</b><span class="live">Running on port 5000</span></li>
    </ol>

    <dl>
      <dt>Container ID</dt><dd>{{ hostname }}</dd>
      <dt>Application</dt><dd>Docker ECR CI/CD Demo</dd>
      <dt>Health check</dt><dd><a href="/health">/health</a></dd>
    </dl>
  </main>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE, hostname=socket.gethostname())


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "Docker ECR CI/CD Demo",
        "hostname": socket.gethostname()
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
function copyInstall(btn) {
  const code = btn.parentElement.querySelector("code").innerText;
  navigator.clipboard.writeText(code).then(() => {
    btn.textContent = "copied ✓";
    setTimeout(() => (btn.textContent = "copy"), 1600);
  });
}

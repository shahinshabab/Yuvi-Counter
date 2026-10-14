"use strict";
const alphabet = document.body.dataset.mode === "alphabet";
const limit = alphabet ? 25 : Number.MAX_SAFE_INTEGER;
let count = 0;
const value = document.getElementById("value");
const plus = document.getElementById("plus");
const minus = document.getElementById("minus");
function render() {
  value.textContent = alphabet ? String.fromCharCode(65 + count) : String(count);
  minus.disabled = count === 0;
  plus.disabled = count === limit;
  if (alphabet) document.getElementById("hint").textContent = `Letter ${count + 1} of 26`;
}
plus.addEventListener("click", () => { count = Math.min(limit, count + 1); render(); });
minus.addEventListener("click", () => { count = Math.max(0, count - 1); render(); });
document.getElementById("reset").addEventListener("click", () => { count = 0; render(); });
render();

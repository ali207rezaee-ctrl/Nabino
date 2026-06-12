async function loadMessages() {
  const res = await fetch("/messages");
  const data = await res.json();

  const box = document.getElementById("chat-box");
  box.innerHTML = "";

  data.forEach(msg => {
    const div = document.createElement("div");
    div.classList.add("msg");

    if (msg.role === "user") {
      div.classList.add("user");
      div.innerText = "👤: " + msg.text;
    } else {
      div.classList.add("admin");
      div.innerText = "👨🏻‍💻 ادمین: " + msg.text;
    }

    box.appendChild(div);
  });

  box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("message");
  const text = input.value;

  if (!text) return;

  await fetch("/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  input.value = "";
  loadMessages();
}

setInterval(loadMessages, 2000);
loadMessages();

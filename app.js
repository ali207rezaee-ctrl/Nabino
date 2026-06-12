const user_id = Telegram.WebApp.initDataUnsafe.user.id;

async function loadMessages() {
  const res = await fetch("/messages");
  const data = await res.json();

  const box = document.getElementById("chat-box");
  box.innerHTML = "";

  data.forEach(m => {
    const div = document.createElement("div");
    div.classList.add("msg");

    if (m.role === "user") {
      div.classList.add("user");
      div.innerText = "👤: " + m.text;
    } else {
      div.classList.add("admin");
      div.innerText = "👨🏻‍💻: " + m.text;
    }

    box.appendChild(div);
  });

  box.scrollTop = box.scrollHeight;
}

async function sendMessage() {
  const input = document.getElementById("message");

  if (!input.value) return;

  await fetch("/send", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      text: input.value,
      user_id: user_id
    })
  });

  input.value = "";
  loadMessages();
}

setInterval(loadMessages, 2000);
loadMessages();

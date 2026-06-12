async function sendMessage() {
    let input = document.getElementById("msg");

    let message = input.value;

    let user = Telegram?.WebApp?.initDataUnsafe?.user;

    if (!user) {
        alert("این فقط داخل تلگرام کار می‌کند");
        return;
    }

    if (!message.trim()) return;

    try {
        await fetch("https://nab-net-bot-production.up.railway.app/send", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                user_id: user.id
            })
        });

        input.value = "";

    } catch (err) {
        console.log("ERROR:", err);
    }
}

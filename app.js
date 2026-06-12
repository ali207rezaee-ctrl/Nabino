async function sendMessage() {
    let input = document.getElementById("msg");

    let message = input.value;

    let user = Telegram.WebApp.initDataUnsafe.user;

    await fetch("https://YOUR-SERVER-URL/send", {
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
}

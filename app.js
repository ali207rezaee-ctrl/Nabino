const chat = document.getElementById("chat");

function addMsg(text,type){
chat.innerHTML += `
<div class="msg ${type}">${text}</div>
`;
chat.scrollTop = chat.scrollHeight;
}

async function send(){
let input = document.getElementById("msg");
let text = input.value;
if(!text) return;

addMsg(text,"me");
input.value="";

const userId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id;

try{
await fetch("https://YOUR_SERVER_URL/sendMessage", {
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
message:text,
user_id:userId
})
});

addMsg("⏳ ارسال شد به پشتیبانی...","support");

}catch(e){
addMsg("❌ خطا در ارسال پیام","support");
}
}

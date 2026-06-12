const chat = document.getElementById("chat");

function addMsg(text,type){
chat.innerHTML += `
<div class="msg ${type}">${text}</div>
`;
chat.scrollTop = chat.scrollHeight;
}

function send(){
let input = document.getElementById("msg");
let text = input.value;
if(!text) return;

addMsg(text,"me");
input.value="";

/* حالت نمایشی */
setTimeout(()=>{
addMsg("💬 پیام شما به پشتیبانی ارسال شد","support");
},500);
}

var socket = io.connect("http://127.0.0.1:80")

console.log("hello")

document.querySelector("#holiday").addEventListener("click",function(){
    socket.emit("hello")
    console.log("HOLIDAY!!!!!!!!!!!")
})
socket.on("got",()=>{
    console.log("recieved from backend")
})

document.querySelector(".ri-menu-4-fill").addEventListener("click",function(){
    document.querySelector("#o").style.transform = "translate(0%)"
    
})

document.querySelector(".ri-close-fill").addEventListener("click",function(){
    document.querySelector("#o").style.transform = "translate(100%)"
})
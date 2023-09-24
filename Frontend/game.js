const socket = new WebSocket("ws://localhost:5500");

socket.addEventListener('open',function (event){
console.log("Connected to WS server");
});

socket.addEventListener('close',function (event){
console.log("DisConnected to WS server");
});

var systemData_g={};
socket.addEventListener('message',function (event){
receivedData=event.data;
const parsedData=JSON.parse(receivedData);
systemData=parsedData['systemData']
gameData=parsedData['gameData']
if (gameData!=undefined)
console.log("Game Data:"+gameData);
if (systemData!=undefined && (systemData['result'] != undefined ||systemData['result']!= ""))
console.log("System Data:"+systemData['result'],systemData['groupId']);
systemData_g=systemData
})

requestTepmplate={'user_details':'','request':{'action':''}}

function createGroup(){
    user_id=document.querySelector("#user").value;
    if(user_id=='')
    {
        return false;
    }


	data=requestTepmplate
	data['request']['action']='createGroup'
	data['user_details']={'user_id':user_id}
    console.log(data);
    socket.send(
        JSON.stringify(data)
        );
    console.log(systemData_g);
    document.querySelector("#genGroupId").innerText=systemData_g['groupId'];
    }

function joinGroup(groupId){
    data=requestTepmplate
	data['request']['action']='joinGroup'
	data['user_details']={'user_id':user_id,'groupId':groupId}
    console.log(data);
    socket.send(
        JSON.stringify(data)
        );
        document.querySelector(".groupSettings").innerHTML="";
    }

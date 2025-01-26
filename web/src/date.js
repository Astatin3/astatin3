let now = new Date()
function format_time(Millis){
  const date = new Date(Millis)

  if(date.getDate() != now.getDate()){
    return date.getMonth()+1 + "/" + date.getDate() + "/" + date.getFullYear()
  }else{
    var Hour = ""
    var Minute = ""
    var AmPm = ""

    if(date.getHours() == 0){
      Hour = "12"
      AmPm = "AM"
    }else if(date.getHours() < 12){
      Hour = date.getHours()
      AmPm = "AM"
    }else if(date.getHours() == 12){
      Hour = "12"
      AmPm = "PM"
    }else{
      Hour = date.getHours() - 12
      AmPm = "PM"
    }

    if(date.getMinutes() < 10){
      Minute = "0" + date.getMinutes()
    }else{
      Minute = date.getMinutes()
    }

    return Hour + ":" + Minute + " " + AmPm

  }
}

times = document.body.getElementsByClassName("format-time")
for(let i=0;i<times.length;i++){
    times[i].innerText = format_time(Number(times[i].innerText)*1000)
}
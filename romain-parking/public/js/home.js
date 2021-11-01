const btn1 = document.querySelector('#curloc');
btn1.onclick = function () {
    navigator.geolocation.getCurrentPosition(
        (position) => {
            // console.log('/find/' + position.coords.latitude + '/' + position.coords.longitude);
            location.href = '/find/' + position.coords.latitude + '/' + position.coords.longitude;
        },
        (errobj) => {
            console.log("Error in getting position!");
            location.href = errobj.message;
        }, {
            enableHighAccuracy: true,
            maximumAge: 10000
        });
};

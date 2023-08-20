document.addEventListener('DOMContentLoaded', function(){

    //boton follow and unfollow
    const followButtons = document.querySelectorAll('.follow');

    // Agrega un event listener a cada botón
    followButtons.forEach(button => {

        button.addEventListener('click', function(){
            var csrftoken = getCookie("csrftoken");
            const id_user = this.getAttribute("data-idfollowing");
            var follow_following = document.querySelector('#follow').innerHTML;
            console.log(id_user);

            fetch(`/user/${id_user}`,{
                method : "PUT",
                headers: {
                    "X-CSRFToken": csrftoken 
                },
                body: JSON.stringify({
                    state : follow_following
                })
            })
            .then(response => response.json())
            .then(data => {
                document.querySelector('#follow').innerHTML = data['content'];
                console.log(data['content'] );
});
        });
    })

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            var cookies = document.cookie.split(";");
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})
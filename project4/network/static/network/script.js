document.addEventListener('DOMContentLoaded', function(){

    //boton follow and unfollow
    const followButtons = document.querySelectorAll('.follow');

    // Agrega un event listener a cada botón
    followButtons.forEach(button => {

        button.addEventListener('click', function(){

            var follow_following = this.getAttribute("data-state");
            console.log(id_user);

            fetch(`/user/${id_user}`,{
                method : "POST",
                headers: {
                    'Content-Type': 'application/json',
                  },
                body: JSON.stringify({
                    state : follow_following
                })
            })
            .then(response => response.json())
            .then(data => {
                this.innerHTML = data['content'];
                console.log(data['content'] );
                window.location.reload();
                
});
        });
    })

})
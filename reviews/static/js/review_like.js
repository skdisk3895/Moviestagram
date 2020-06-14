
const buttons = document.querySelectorAll('.js-like-button')

buttons.forEach(function(button) {
    button.addEventListener('click', function(event) {
        const reviewPk = event.target.dataset.review_pk
        axios.get(`/reviews/${reviewPk}/like/`)
        .then(res => {
            const reviewLikeCount = document.querySelector(`#reviewLikeCount${reviewPk}`)
            if (res.data.is_liked) {
                event.target.style.color = "red"
            } else {
                event.target.style.color = "black"
            }
            reviewLikeCount.innerText = res.data.like_count
        })
    })
})
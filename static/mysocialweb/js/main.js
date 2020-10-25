
const arrowBtn = document.querySelector('.arrow');
const arrowIcon = document.querySelector('.fa-arrow-down');
const img = document.querySelector('.item1');


arrowBtn.addEventListener('click', function (){
    img.classList.toggle('hide');
    console.log(img)

if (img.classList.contains('hide')) {
    arrowIcon.style.transform = 'rotate(180deg)'
} else {
    arrowIcon.style.transform = 'rotate(0deg)'
};
});
import Cropper from 'cropperjs';

const toggleSideBar = document.getElementById("toggle-side-bar")
const mainPage = document.getElementById("main-page")
const sidebar = document.getElementById("side-bar")
const mainNav = document.getElementById("main-nav")
const dropdownToggles = document.querySelectorAll(".dropdown-toggle")
const mainOverlay = document.querySelector("#main-overlay")
const overlayToggles = document.querySelectorAll(".overlay-toggle")

// Activate the active sidebar item
if (sidebar != null) {
    const target = sidebar.dataset.active
    if (target != null) {
        document.getElementById(target)?.classList.add("active")
    }
}


if (toggleSideBar != null) {
    toggleSideBar?.addEventListener("click", () => {
        sidebar?.classList.toggle("collapsed")
        mainPage?.classList.toggle("collapsed")
    })
}

// Raise/Lower the main navbar
window.addEventListener("scroll", () => {
    if (window.scrollY > 100) {
        mainNav?.classList.add("raised")
    } else {
        mainNav?.classList.remove("raised")
    }
})

// Form validation
window.addEventListener('load', function () {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})

if (dropdownToggles != null) {
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener("click", () => {
            const target = toggle.dataset.target
            toggle.parentElement.querySelector(target).classList.toggle("active")
            mainOverlay?.classList?.toggle("active")
        })
    })
}

// Use the main page overlay to close the dropdown and toggle  menus
mainOverlay?.addEventListener("click", () => {
    overlayToggles?.forEach(object => {
        object.classList.remove("active")
        mainOverlay.classList.remove("active")
    })
});

// Deletion
const confirmationForms = document.querySelectorAll(".requires-confirmation")
confirmationForms?.forEach(form => {
    const message = form.dataset.message
    form.addEventListener("submit", event => {
        const response = confirm(message)
        if (!response) {
            event.preventDefault()
        }
    })
})


// DataTable
$(document).ready(function () {
    document.querySelectorAll(".data-table").forEach(table => {
        $(table).DataTable()
    })
});

// Editor
document.querySelectorAll(".ckeditor")?.forEach(editor => {
    CKEDITOR.replace(editor.getAttribute("id"));
})

// Cropping
const croppableContainers = document.querySelectorAll(".croppable-container")
croppableContainers?.forEach(container => {
    const image = container.querySelector('img');
    const dataContainer = container.querySelector('.cropdata');
    if (image != null && dataContainer != null) {
        let aspectRatio = image.dataset.aspectRatio
        if (aspectRatio != null && aspectRatio != undefined && aspectRatio != "") {
            aspectRatio = aspectRatio.split(":").map(x => parseInt(x))
            aspectRatio = aspectRatio[0] / aspectRatio[1]
        } else {
            aspectRatio = null
        }
        new Cropper(image, {
            aspectRatio: aspectRatio,
            crop(event) {
                const data = `${event.detail.x},${event.detail.y},${event.detail.width},${event.detail.height},${event.detail.rotate},${event.detail.scaleX},${event.detail.scaleY}`
                dataContainer.setAttribute("value", data)
            },
        });
    }
})


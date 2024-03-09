
$(document).ready(function(){get_structure_type();add_styles();})
function hide_ul(){
        let toggle_flag = true;
    $('.filter_panel').find("ul").click(function () {
        toggle_flag = ! toggle_flag;
        $('ul').each(function(){
            $(this).slideToggle(toggle_flag);
        });
    });
}
function add_styles(){
    let widget_list =['input','textarea','select']
    for (const widget_name of widget_list) {
        const selector = document.querySelectorAll(widget_name)
        for (const val of selector) {
            if (val.type==='checkbox'){
                val.classList.add("form-check-input");
        }
            else {
                val.classList.add("form-control");
        }
    }
}
}
function get_structure_type(){
    const id_structure_type =document.getElementById('id_structure_type')
    if (id_structure_type)
    id_structure_type.addEventListener('change', function () {
    const url_data = "{% url 'HeatAndVentilation:filter_base_structure' %}"
    let endpoint = $("#js-products").attr("data-url");
    console.log(endpoint?endpoint:url_data)
    let category_id = this.value;
    $.ajax({
        type: 'GET',
        url: endpoint?endpoint:url_data,
        data: { 'category': category_id },
        dataType: 'json',
        success: function (data) {
            let courseSelect = document.getElementById('id_base_structures');
            courseSelect.innerHTML = '';
            data.forEach(function (course) {
                let option = document.createElement('option');
                option.value = course.id;
                option.text = course.name;
                courseSelect.add(option);
            });
        }
    });
})
    }
function filter_panel(){
    let filter_panel = $('.filter_panel')
    filter_panel.find("span").each(function(){
        let $title = $(this);
        // $title.next().toggle();
        $title.css("cursor","pointer");
        $title.click(function(){
            $title.next().slideToggle();
        });
    });
}


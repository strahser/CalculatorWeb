$(document).ready(function(){create_elements(); create_ajax();add_ajax_to_modal()})
const target_url_="{% url 'HeatAndVentilation:check_thermal_resistence' %}"
function create_elements() {
    $('<button type="button" class="btn btn-primary" id="add-html-button" data-bs-toggle="modal" data-bs-target="#exampleModal"> Рассчитать терм.сопр. </button>')
        .insertAfter('#id_R_custom');
    $('<div id="html_target" ></div>').insertAfter($('#id_standard_structure_type'));
}
function create_modal_body(data_parse){
        function save_modal_button_handler(data_parse){
        $("#id_standard_structure_type").val(data_parse.R_calc);
        $("#id_thickness").val(data_parse.sum_thickness)
        $("#exampleModal").modal('toggle')
        $("#html_target").html(data_parse.df_);
    }
        const modal_data =`
        <p> Тип конструкции ${$('#id_standard_structure_type option:selected').text()}</>
        <p>Расчетное терм.сопр.: ${data_parse.R_calc}</p>
        <p>Суммарная толщина конструкции,мм.: ${data_parse.sum_thickness}</p>
        <p>Номируемые термические сопротивления,мм.: ${data_parse.gsop_list}</p>
        `
        // Adding the data to the modal
        $('.modal-body').html(modal_data);
        $("#save_modal").on('click',function(){save_modal_button_handler(data_parse)});
        $("#close_modal").on('click',function(){$("#html_target").html(data_parse.df_)});
    }
function data_ajax(){
    const wall_type = $('#id_standard_structure_type').val();
    // const all_layers = Array.from(document.getElementById('id_structure_layer_to').options).map(option => parseInt(option.value));
    const all_layers =[1,2]
    const selected_building =  Array.from(document.getElementById('id_buildings_list_to').options).map(option => parseInt(option.value));
        console.log(selected_building,wall_type)
    return {
    'structure_type': wall_type, 'all_layers': all_layers, 'selected_building': selected_building,
    csrfmiddlewaretoken: '{{ csrf_token }}'
    };
}
function create_ajax(){
    $.ajax({
        url: target_url_,
        data: {data:"data"},
        async:false,
        type: "GET",
        dataType: 'html',
        success: function (responce) {
            if (responce) {
                const data_parse = JSON.parse(responce);
                // $("#html_target").html(data_parse)
                console.log("{{ request.get_full_path }}")
            }
        },
    }
    );
}
function add_ajax_to_modal(){
     $("#add-html-button").on('click',
         function (){
         $.ajax({
        url: target_url_,
        data: data_ajax(),
        async:false,
        type: "GET",
        dataType: 'html',
        success: function (responce) {
            if (responce) {
                const data_parse = JSON.parse(responce);
                create_modal_body(data_parse)
                $("#html_target").html(data_parse.df_)
            }
        },
    }
    );
         }
     );
}
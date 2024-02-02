function findTotal(){
    let thickness = document.getElementById('id_thickness');
    let lambda_structure = document.getElementById('id_lambda_structure');
    let option_value =document.getElementById('id_standard_structure_type')
    if (option_value.value === 'Wall') {
        let tot = 1 / 23 + (parseFloat(lambda_structure.value) / parseFloat(thickness.value)) + 1 / 8.7;
        document.getElementById('id_R_real').value = tot;
    } else {
        tot = parseFloat(lambda_structure.value) / parseFloat(thickness.value);
        document.getElementById('id_R_real').value = tot;
    }
}
function functionAddAttribute(){
    let arr = ['id_lambda_structure', 'id_thickness', 'id_standard_structure_type']
    let temp;
    for (let val in arr) {
        temp = document.getElementById(val)
        if (temp) {
            temp.setAttribute('onchange', 'findTotal()');
        }
    }
}
function calculate_R_real() {
    let selected_fields = document.getElementById('id_structure_layer_to');
    console.log(selected_fields.value);

}
function onChange() {
        let optionals = Array.from(document.getElementById('id_structure_layer_to').options).map(option => parseInt(option.value));
        let R_real = document.getElementById('id_R_real')
        R_real.value = optionals.reduce((a, b) => a + b, 0)
    }
    function autoload(){
        let all_options = document.getElementById('id_structure_layer_to');
        let wall_option_value = document.getElementById('id_standard_structure_type');
        all_options.setAttribute('onchange','onChange()');
        wall_option_value.setAttribute('onchange','onChange()');
        console.log(wall_option_value.value)
    }

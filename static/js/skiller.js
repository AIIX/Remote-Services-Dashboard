//               $('skillForm').onSubmit((form)=>{
//                    const a = new FormData(form);
//                    $.post("{{ url_for('on_skill_settings_changed') }}",  {form_data: a});
//                })

function generateSkillDisplay(skills_model) {
    var accordion = document.getElementById("skills_accordion")
    for (var i = 0; i < skills_model.length; i++){
        var json = skills_model[i].settings_meta;
        var sections = json.skillMetadata.sections
        buildSkillsCard(sections, skills_model[i].skill_name)
        //getFormFields(json.type);
    }
}

function buildSkillsCard(sections, skill_name)
{
var original_skill_name = skill_name
var skill_name = skill_name.split(".")[0]
var accordion = document.getElementById("skills_accordion")
var accordion_card_div = document.createElement('div')
var accordion_card_header_div = document.createElement('div')
var accordion_card_header_skillheader = document.createElement('h3')
var accordion_card_header_skillheader_arrows = document.createElement('span')
var accordion_card_collapse_div = document.createElement('div')
var accordion_card_body_div = document.createElement('div')
var accordion_card_body_section_div = document.createElement('div')
var accordion_card_header_sectionheader_div = document.createElement('div')
var accordion_card_body_section_header = document.createElement('h4')
var accordion_card_body_section_form = document.createElement('div')

// Create Parent Element: Card Div
accordion_card_div.id = skill_name + "_card"
accordion_card_div.className = "card bg-dark text-white"

// Create Child Element: Card Header Div
accordion_card_header_div.id = skill_name + "_card_header"
accordion_card_header_div.className = "card-header bg-dark row"
accordion_card_header_div.setAttribute("data-toggle", "collapse")
accordion_card_header_div.setAttribute("data-target", "#" + skill_name + "_collapse")
accordion_card_header_div.setAttribute("aria-expanded", "false")
accordion_card_header_div.setAttribute("aria-controls", skill_name + "_collapse")

// Create Child Element: Card Header H3 Element
accordion_card_header_skillheader.id = skill_name + "_card_skillheader"
accordion_card_header_skillheader.className = "font-weight-bold text-uppercase col-sm-11"
accordion_card_header_skillheader.innerHTML = skill_name.replace("-", " ")

accordion_card_header_skillheader_arrows.className = "accord-header-link col-sm-1 h-100"

// Add Card Header H3 Element To Card Header Div
accordion_card_header_div.appendChild(accordion_card_header_skillheader)
accordion_card_header_div.appendChild(accordion_card_header_skillheader_arrows)

// Add Card Header Div to Card Div
accordion_card_div.appendChild(accordion_card_header_div)

// Create Child Element: Card Collapse Div
accordion_card_collapse_div.id = skill_name + "_collapse"
accordion_card_collapse_div.className = "collapse"
accordion_card_collapse_div.setAttribute("data-parent", "#skills_accordion")
accordion_card_collapse_div.setAttribute("aria-labelledby", accordion_card_header_div.id)

// Create Child Element: Card Body Div
accordion_card_body_div.id = skill_name + "_body"
accordion_card_body_div.className = "card-body p-3 text-center"

sections.forEach(section =>  {
	// Create Child Element: Card Body Section Div
	accordion_card_body_section_div.id = section.name + "_id"
	accordion_card_body_section_div.className = "card-header bg-dark"

	// Create Child Element: Card Header Section Header Div Element
    accordion_card_header_sectionheader_div.className = "d-block p-2 m-2 bg-danger text-white"

	// Create Child Element: Card Section Header H4 Element
	accordion_card_body_section_header.id = section.name + "_header"
	accordion_card_body_section_header.className = "font-weight-bold text-uppercase"
	accordion_card_body_section_header.innerHTML = section.name

    accordion_card_header_sectionheader_div.appendChild(accordion_card_body_section_header)

	// Add Card Section Header H4 Element to Card Section Div
	accordion_card_body_section_div.appendChild(accordion_card_header_sectionheader_div)

    // Create Child Element: Card Section Form
    accordion_card_body_section_form.id = section.name + "_form"
    accordion_card_body_section_form.className = "bg-dark"

	// Get & Build Form Fields
	var generated_section_form_fields = getFormFields(section.fields, original_skill_name)
	//console.log(generated_section_form_fields)
	accordion_card_body_section_form.appendChild(generated_section_form_fields)

    // Add Card Section Form To Card Section Div
    accordion_card_body_section_div.appendChild(accordion_card_body_section_form)

	// Add Card Section Div to Card Body Div
	accordion_card_body_div.appendChild(accordion_card_body_section_div)
})

// Add Card Body to Card Collapse Div
accordion_card_collapse_div.appendChild(accordion_card_body_div)

// Add Card Collapse Div to Card Div
accordion_card_div.appendChild(accordion_card_collapse_div)

// Add Card Div to Accordion
accordion.appendChild(accordion_card_div)
}

function getFormFields(fields, original_skill_name) {
    var skill_form_name = original_skill_name.split(".")[0] + "_form"
    var skill_form_id = skill_form_name + "_id"
    var skill_form_class = skill_form_name + "_class"

    var accordion_card_form_div = document.createElement('div')
    var accordion_card_form = document.createElement('form')
    var accordion_card_form_button = document.createElement('button')

    accordion_card_form.id = skill_form_id
    accordion_card_form.className = skill_form_class
    accordion_card_form.setAttribute("name", skill_form_name)
    accordion_card_form.setAttribute("method", "POST")
    function handleForm(event) { submit_sub_form(original_skill_name, skill_form_class, skill_form_id);  event.preventDefault(); }
    accordion_card_form.addEventListener("submit", handleForm)
//    accordion_card_form.setAttribute("action", submit_sub_form(original_skill_name, skill_form_class, skill_form_id))
//    accordion_card_form.onSubmit = submit_sub_form(original_skill_name, skill_form_class, skill_form_id)

    //accordion_card_form_div.appendChild(accordion_card_form)
    //let formHtml = $('<div></div>')//$('<form name=${skill_form_name} method="" class=${skill_form_class} onsubmit="submit_sub_form(${original_skill_name}, ${skill_form_class}, ${skill_form_id})"></form>');
    //formHtml.append(accordion_card_form_div.innerHTML)
    fields.forEach(field => {
        //console.log(field)
        //formHtml.append(getRenderedField(field));
        accordion_card_form.appendChild(getRenderedField(field));
    })
    //accordion_card_form.append('<button class="btn btn-primary btn-lg btn-block" type="submit" >Save</button>')
    accordion_card_form_button.className = "btn btn-primary btn-lg btn-block"
    accordion_card_form_button.type = "submit"
    accordion_card_form_button.innerHTML = "Save"

    accordion_card_form.appendChild(accordion_card_form_button)
    accordion_card_form_div.appendChild(accordion_card_form)

    //formHtml.append('<button class="btn btn-primary btn-lg btn-block" type="submit" >Save</button>')

    //return formHtml.html();
    return accordion_card_form_div;
    //return accordion_card_form.innerHTML;
}

function getRenderedField(field) {
    //console.log(field.type)
    switch(field.type) {
        case 'text':
            return getInputField(field);
        case 'select':
            return getSelectField(field);
        case 'disabled-text-field':
            return getButtonField(field)
        case 'checkbox':
            return getCheckField(field)
        default:
            return getLabelField(field);
    }
}

function getButtonField(field) {
var buttonField_div = document.createElement('div');
buttonField_div.className = "form-group"
buttonField_div.setAttribute('hidden', 'true')
return buttonField_div ///`<div class="form-group" hidden> </div>`;
}

function getCheckField(field) {
console.log("Select Check Log: " + field.name)
var checkField_div = document.createElement("div")
var checkField_div_btn_group = document.createElement("div")
var checkField_button_one = document.createElement("input")
var checkField_label = document.createElement("label")

checkField_div.className = "form-group"
checkField_div_btn_group.className = "form-check"
checkField_button_one.className = "form-check-input check-scale-type"
checkField_button_one.type = "checkbox"
checkField_button_one.value = field.value
checkField_button_one.name = field.name
checkField_label.className = "form-check-label"
checkField_label.setAttribute("for", field.name)
checkField_label.innerHTML = field.label

checkField_div_btn_group.appendChild(checkField_button_one)
checkField_div_btn_group.appendChild(checkField_label)

checkField_div.appendChild(checkField_div_btn_group)

return checkField_div

//return `<div class="form-group">
//<div class="btn-group btn-toggle">
//    <button class="btn btn-lg btn-default active=${field.value}">ON</button>
//    <button class="btn btn-lg btn-primary active=${field.value}">OFF</button>
//</div>
//<label class="form-check-label" for="flexCheckDefault">${field.label}</label>
//</div>`;
}

function getLabelField(field) {
var LabelField_div = document.createElement("div")
var LabelField_h4 = document.createElement("h4")

LabelField_div.className = "form-group"
LabelField_h4.innerHTML = field.label

LabelField_div.appendChild(LabelField_h4)

return LabelField_div
//return `<div class="form-group">
//<h4>${field.label}</h4>
//</div>`;
}

function getInputField(field) {
    console.log("Input Field Log: " + field.name)
    var card_input_field_form = document.createElement('div')
    var card_input_form_group = document.createElement('div')
    var card_input_form_group_prepend = document.createElement('div')
    var card_input_form_group_label = document.createElement('span')
    var card_input_form_group_input = document.createElement('input')

    card_input_form_group.className = "form-group input-group input-group-lg"
    card_input_form_group_prepend.className = "input-group-prepend"
    card_input_form_group_label.innerHTML = field.label
    card_input_form_group_label.className = "text-capitalize input-group-text"
    card_input_form_group_label.setAttribute("for", field.name)
    card_input_form_group_input.id = field.name
    card_input_form_group_input.className = "form-control"
    card_input_form_group_input.name = field.name

    card_input_form_group_prepend.appendChild(card_input_form_group_label)
    card_input_form_group.appendChild(card_input_form_group_prepend)
    card_input_form_group.appendChild(card_input_form_group_input)
    card_input_field_form.appendChild(card_input_form_group)

    return card_input_field_form //.innerHTML

//   return `<div class="form-group">
//    <label for="exampleInputEmail1">${field.label}</label>
//    <input type="text" class="form-control" id="${field.name}">
//    <small class="error"><i class="fa fa-info"></i> Please validate this input</small>
//  </div>`;
}


function getSelectField(field) {
   console.log("Select Field Log: " + field.name)
   const option_keys = getOptions(field.options);
   var card_select_field_form = document.createElement('div')
   var card_select_form_group = document.createElement('div')
   var card_select_form_group_prepend = document.createElement('div')
   var card_select_form_group_label = document.createElement('span')
   var card_select_form_group_select = document.createElement('select')

   card_select_form_group.className = "form-group input-group input-group-lg"
   card_select_form_group_prepend.className = "input-group-prepend"
   card_select_form_group_label.innerHTML = field.label
   card_select_form_group_label.className = "text-capitalize input-group-text"
   card_select_form_group_label.setAttribute("for", field.name)
   card_select_form_group_select.className = "form-control"
   card_select_form_group_select.name = field.name

   card_select_form_group_prepend.appendChild(card_select_form_group_label)
   card_select_form_group.appendChild(card_select_form_group_prepend)

   option_keys.forEach(option => {
        var opt = document.createElement("option");
        opt.textContent = option.split("|")[0]
        opt.value = option.split("|")[1]
        if(field.value == option.split("|")[1]){
            opt.setAttribute("selected", "selected")
        }
        card_select_form_group_select.append(opt)
   })

   card_select_form_group.appendChild(card_select_form_group_select)
   card_select_field_form.appendChild(card_select_form_group)

   return card_select_field_form //.innerHTML
}

function getOptions(options) {
    const optionsList = options.split(';');

    optionsList.forEach(option => {
        const value = option.split('|')[0];
    });

    return optionsList
}

function serialize (data) {
	let obj = {};
	for (let [key, value] of data) {
		if (obj[key] !== undefined) {
			if (!Array.isArray(obj[key])) {
				obj[key] = [obj[key]];
			}
			obj[key].push(value);
		} else {
			obj[key] = value;
		}
	}
	return obj;
}

function submit_sub_form(original_skill_name, skill_form_class, skill_form_id) {
    console.log(original_skill_name)
    console.log(skill_form_class)
    var form_element_to_fetch = document.querySelector("#" + skill_form_id)
    var form_data = new FormData(form_element_to_fetch)
    var serialized = serialize(form_data)
    var to_send = JSON.stringify(serialized)
    $.post(submit_settings_url,  {form_data: to_send, skill_name: original_skill_name});
}
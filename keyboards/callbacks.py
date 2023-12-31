from aiogram.utils.callback_data import CallbackData


#User
replenishment = CallbackData('replenishment', 'current_user')
check_replenishment = CallbackData('check', 'id', 'current_user')

privilege = CallbackData('privilege', 'name', 'current_user')
purchase_type = CallbackData('purchase_type', 'name', 'current_user')
bay_privilege = CallbackData('bay_privilege', 'name', 'type', 'current_user')

back_bay = CallbackData('back_bay', 'current_user')

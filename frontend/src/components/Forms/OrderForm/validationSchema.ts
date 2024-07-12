import {object, string, array} from 'yup'


export const orderValidSchema = object({
    name: string().required("Ім'я - обов'язкове"),
    surname: string().required("Прізвище - обов'язкове"),
    email: string().required("Email - обов'язковий").email('Перевірте правильність введення email'),
    phone: string(),
    order_items: array().min(1, 'Для оформлення замовлення потрібно додати до кошика хоча б один товар'),
})
import { Currency } from "../models/entities";

export const formatCurrency = (input: Currency) => {
    switch(input){
        case 'UAH': 
        // return '₴'
        return 'грн'
        case 'EUR': return '€'
        case 'USD': return '$'
        default: return ''
    }
}
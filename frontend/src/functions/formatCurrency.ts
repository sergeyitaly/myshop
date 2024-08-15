
import { Currency } from '../models/entities';

export const formatCurrency = (currency: Currency): string => {
    switch (currency) {
        case 'UAH':
            return '₴'; // Ukrainian Hryvnia symbol
        case 'USD':
            return '$'; // US Dollar symbol
        case 'EUR':
            return '€'; // Euro symbol
        default:
            return '$'; // Default to US Dollar symbol
    }
};
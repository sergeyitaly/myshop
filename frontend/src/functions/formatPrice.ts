import { Currency } from "../models/entities"
import { formatCurrency } from "./formatCurrency"
import { formatNumber } from "./formatNumber"

export const formatPrice = (number: string | number, currency: Currency) => {
    return `${formatNumber(number)} ${formatCurrency(currency)}`
}
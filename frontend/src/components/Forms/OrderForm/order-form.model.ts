import { BasketItemModel } from "../../../models/entities"

export interface OrderFormModel {
    firstName: string
    lastName: string
    phone: string
    email: string
    isAnotherRecipient: boolean
    comment: string
    isPresent: boolean
    products: BasketItemModel[]
    totalPrice: number
}

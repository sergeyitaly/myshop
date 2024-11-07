import { array, number, object } from "yup";
import { FeedbackForm } from "../../models/entities";

export const initialFormData: FeedbackForm = {
    email: '',
    name: '',
    comment: '',
    ratings: [] 
}


export const validationSchema = array().of(object({rating: number().min(1, 'Rating must be greater than or equal to 1').max(4)}))
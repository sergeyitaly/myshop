import { ENDPOINTS } from "../constants";
import { FeedbackForm } from "../models/entities";
import { apiSlice } from "./mainApiSlice";

export interface CreateOrderErrorResponce {
    status: number
    data: {
        name: string
    }
}

export const feedbackApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        createFeedback: builder.mutation<string, FeedbackForm>({
            query: (body) => ({
                body,
                method: 'POST',
                url: `${ENDPOINTS.FEEDBACK}/`
            }),
            transformErrorResponse: (baseQueryReturnValue: CreateOrderErrorResponce) => {
                return baseQueryReturnValue
            },
        })
    })
})

export const {
    useCreateFeedbackMutation
} = feedbackApiSlice
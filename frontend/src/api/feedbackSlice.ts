import { ENDPOINTS } from "../constants";
import { FeedbackForm, Question } from "../models/entities";
import { ShortServerResponce } from "../models/server-responce";
import { apiSlice } from "./mainApiSlice";

export interface CreateFeedbackErrorResponse {
    status: number;
    data: {
        name?: string; 
        email?: string; 
        comment?: string; 
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
            transformErrorResponse: (baseQueryReturnValue: CreateFeedbackErrorResponse) => {
                const { status, data } = baseQueryReturnValue;
                return { status, errors: data };             },
        }),
        getAllQuestions: builder.query<ShortServerResponce<Question[]>, void>({
            query: () => {
              return `${ENDPOINTS.QUESTIONS}/`;
            }
          }),
    })
})

export const {
    useCreateFeedbackMutation,
    useGetAllQuestionsQuery
} = feedbackApiSlice
import { FeedbackCard } from "../../components/Cards/FeedbackCard/FeedbackCard"
import { PageContainer } from "../../components/containers/PageContainer"
import { MainButton } from "../../components/UI/MainButton/MainButton"
import styles from './Feedback.module.scss'
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"
import { useEffect, useState } from "react"
import { FeedbackForm } from "../../models/entities"
import { useCreateFeedbackMutation, useGetAllQuestionsQuery } from "../../api/feedbackSlice"
import clsx from "clsx"
import { AppModal } from "../../components/AppModal/AppModal"
import { FeedbackModalForm } from "./FeedbackForm/FeedbackModalForm"
import { useToggler } from "../../hooks/useToggler"
import { useAppTranslator } from "../../hooks/useAppTranslator"



export const FeedbackPage = () => {

    const navigate = useNavigate()

    const {openStatus, handleClose, handleOpen} = useToggler()

    const {t} = useAppTranslator()

    const {data} = useGetAllQuestionsQuery()


    const [form, setForm] = useState<FeedbackForm>({
        email: '',
        name: '',
        comment: '',
        ratings: []
    })

    useEffect(() => {
        if(data) {
            const questionsTemplates = data.results.map(({id, aspect_name}) => ({
                question_id: id,
                answer: '',
                rating: aspect_name ? 0 : undefined 
            }))

            setForm({...form, ratings: questionsTemplates })
        }
    }, [data]) 


    const [sendForm, {isLoading, isSuccess}] = useCreateFeedbackMutation()

    useEffect (() => {
        isSuccess && navigate(ROUTE.THANK_FOR_FEEDBACK)
    }, [isSuccess])

    const handleClick = (id: number, value: number) => {
        const newRating = form.ratings.map((oldRating) => {
            if(oldRating.question_id === id) return {...oldRating, rating: value}
            return oldRating
        })
        setForm({...form, ratings: newRating})
    }

    const handleChange = (id: number, value: string) => {
        const newRating = form.ratings.map((oldRating) => {
            if(oldRating.question_id === id) return {...oldRating, answer: value}
            return oldRating
        })
        setForm({...form, ratings: newRating})
    }

    const handleSubmit = () => {
        sendForm(form)
    }

    const handleChangeHeader = (fieldName: string, value: string) => {
        setForm({...form, [fieldName]: value})
    }

    return (
        <>
        <PageContainer className={clsx({[styles.loading]: isLoading})}>
         
            <div className={styles.intro}>
                <p>{t('greetting')}<span>KOLORYT!</span> </p>
                <p>{t('ask_to_rate')}</p>
                <p>P.S {t('ps')}</p>
            </div>
            <div className={styles.cardContainer}>
                {
                    data?.results.map(({id, aspect_name, question}, index) => (
                        <FeedbackCard
                            key={id}
                            question1={`${index+1}. ${aspect_name ? aspect_name : question}`}
                            question2={aspect_name ? question : ''}
                            showButtons = {aspect_name ? true : false}
                            thisRating={form.ratings.find(({question_id}) => question_id === id)?.rating}
                            onClick={(val) => handleClick(id, val)}
                            onChangeText={(val) => handleChange(id, val)}
                        />
                    ))
                }
            </div>
            <div className={styles.actions}>
                <MainButton
                    color="blue"
                    title={t("send")}
                    onClick={handleOpen}
                />
                <button className={styles.button} onClick={() => navigate(ROUTE.HOME)}>{t('close_and_return')}</button>
            </div>
        </PageContainer>
        <AppModal
            open = {openStatus}
            onClickOutside={handleClose}
        >
            <FeedbackModalForm
                isLoading = {isLoading}
                onSubmit={handleSubmit}
                onChange={handleChangeHeader}
            />
        </AppModal>
        </>
    )
}
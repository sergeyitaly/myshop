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



export const FeedbackPage = () => {

    const navigate = useNavigate()

    const {openStatus, handleClose, handleOpen} = useToggler()

    const {data} = useGetAllQuestionsQuery()


    const [form, setForm] = useState<FeedbackForm>({
        email: '',
        name: '',
        comment: '',
        ratings: []
    })

    useEffect(() => {
        if(data) {
            const questionsTemplates = data.results.map(({id}) => ({
                question_id: id,
                answer: '',
                rating: 0
            }))

            setForm({...form, ratings: questionsTemplates })
        }
    }, [data]) 

    console.log(form);
    


    const [sendForm, {isLoading}] = useCreateFeedbackMutation()

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
        handleClose()

    }

    const handleChangeHeader = (fieldName: string, value: string) => {
        setForm({...form, [fieldName]: value})
    }

    return (
        <>
        <PageContainer className={clsx({[styles.loading]: isLoading})}>
         
            <div className={styles.intro}>
                <p>Вас вітає команда - <span>KOLORYT!</span> </p>
                <p>Цей сайт,  ми дуже старанно і довго робили, тому, дуже просимо вас подивитись, оцінити його і можливо залишити пару коментарів - відгуків! Це не займе багато часу а для нас буде дуже приємно! </p>
                <p>P.S Ви також можете поділитись нашим сайтом з друзями і знайомими!</p>
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
                    title="Надіслати"
                    onClick={handleOpen}
                />
                <button className={styles.button} onClick={() => navigate(ROUTE.HOME)}>Закрити і повернутися на головний екран</button>
            </div>
        </PageContainer>
        <AppModal
            open = {openStatus}
            onClickOutside={handleClose}
        >
            <FeedbackModalForm
                onSubmit={handleSubmit}
                onChange={handleChangeHeader}
            />
        </AppModal>
        </>
    )
}
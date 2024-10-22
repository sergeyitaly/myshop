import { FeedbackCard } from "../../components/Cards/FeedbackCard/FeedbackCard"
import { PageContainer } from "../../components/containers/PageContainer"
import { MainButton } from "../../components/UI/MainButton/MainButton"
import styles from './Feedback.module.scss'
import image from './image.png'
import {cards} from './fakeData'
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"
import { useState } from "react"
import { FeedbackForm } from "../../models/entities"
import { useCreateFeedbackMutation } from "../../api/feedbackSlice"
import clsx from "clsx"



const initialForm: FeedbackForm = {
    name: 'Alex',
    comment: 'Comment',
    email: 'aaa@gmail.com',
    ratings: cards.map(({id, ratingButtons}) => ({
            question_id: id,
            answer: '',
            rating: ratingButtons ? 0 : 5
        }) )
}

export const FeedbackPage = () => {

    const navigate = useNavigate()

    const [form, setForm] = useState<FeedbackForm>(initialForm)

    console.log(form.ratings);

    const [sendForm, {isLoading}] = useCreateFeedbackMutation()


    const handleClick = (id: number, value: number) => {
        const newRating = form.ratings.map((oldRating) => {
            if(oldRating.question_id === id) return {...oldRating, rating: value}
            return oldRating
        })
        setForm({...form, ratings: newRating})
    }

    // const handleChange = (id: number, value: string) => {
    //     const newRating = form.ratings.map((oldRating) => {
    //         if(oldRating.question_id === id) return {...oldRating, answer: value}
    //         return oldRating
    //     })
    //     setForm({...form, ratings: newRating})
    // }

    const handleSubmit = () => {
        sendForm(form)
    }

    return (
        <PageContainer className={clsx({[styles.loading]: isLoading})}>
            <div className={styles.imageWrapper}>
                <img 
                    src={image}
                    alt="image" 
                    className={styles.image}
                />
            </div>
            <div className={styles.intro}>
                <p>Вас вітає команда - <span>KOLORYT!</span> </p>
                <p>Цей сайт,  ми дуже старанно і довго робили, тому, дуже просимо вас подивитись, оцінити його і можливо залишити пару коментарів - відгуків! Це не займе багато часу а для нас буде дуже приємно! </p>
                <p>P.S Ви також можете поділитись нашим сайтом з друзями і знайомими!</p>
            </div>
            <div className={styles.cardContainer}>
                {
                    cards.map(({id, firstQuestion, secondQuestion, ratingButtons}, index) => (
                        <FeedbackCard
                            key={id}
                            question1={`${index+1}. ${firstQuestion}`}
                            question2={secondQuestion}
                            showButtons = {ratingButtons}
                            thisRating={form.ratings.find(({question_id}) => question_id === id)?.rating}
                            onClick={(val) => handleClick(id, val)}

                        />
                    ))
                }
            </div>
            <div className={styles.actions}>
                <MainButton
                    color="blue"
                    title="Надіслати"
                    onClick={handleSubmit}
                />
                <button className={styles.button} onClick={() => navigate(ROUTE.HOME)}>Закрити і повернутися на головний екран</button>
            </div>
        </PageContainer>
    )
}
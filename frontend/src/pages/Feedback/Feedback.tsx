import { FeedbackCard } from "../../components/Cards/FeedbackCard/FeedbackCard"
import { PageContainer } from "../../components/containers/PageContainer"
import { MainButton } from "../../components/UI/MainButton/MainButton"
import styles from './Feedback.module.scss'
import image from './image.png'
import {cards} from './fakeData'
import { useNavigate } from "react-router-dom"
import { ROUTE } from "../../constants"



export const FeedbackPage = () => {

    const navigate = useNavigate()

    return (
        <PageContainer>
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
                    cards.map(({firstQuestion, secondQuestion, value}, index) => (
                        <FeedbackCard
                            question1={`${index+1}. ${firstQuestion}`}
                            question2={secondQuestion}
                            showButtons = {value !== null}
                        />
                    ))
                }
            </div>
            <div className={styles.actions}>
                <MainButton
                    color="blue"
                    title="Надіслати"
                />
                <button className={styles.button} onClick={() => navigate(ROUTE.HOME)}>Закрити і повернутися на головний екран</button>
            </div>
        </PageContainer>
    )
}
import { IconButton } from '../../UI/IconButton/IconButton'
import styles from './FeedbackCard.module.scss'

interface FeedbackCardProps {
    question1: string
    question2?: string
    showButtons?: boolean
    onClick?: (value: string) => void
    onChangeText?: (text: string) => void
}

export const FeedbackCard = ({
    question1,
    question2,
    showButtons,
}: FeedbackCardProps) => {
    return (
        <div className={styles.card}>
            <p className={styles.firstQuestion}>{question1}</p>
            {
                showButtons &&
                <div className={styles.buttons}>
                    <IconButton
                        iconName='face1'
                        className={styles.button}  
                    />
                    <IconButton
                        iconName='face2'
                        className={styles.button}  
                    />
                    <IconButton
                        iconName='face3'
                        className={styles.button}  
                    />
                    <IconButton
                        iconName='face4'
                        className={styles.button}  
                    />
                </div>
            }
            {question2 && <p className={styles.secondQusetion}>{question2}</p>} 
            <textarea
                className={styles.textarea}
                placeholder='Ваша відповідь...'
            />
        </div>
    )
}
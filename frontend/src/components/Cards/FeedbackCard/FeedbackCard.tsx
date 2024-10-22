import clsx from 'clsx'
import { IconButton } from '../../UI/IconButton/IconButton'
import styles from './FeedbackCard.module.scss'
import { ChangeEvent } from 'react'

interface FeedbackCardProps {
    question1: string
    question2?: string
    showButtons?: boolean
    thisRating?: number
    onClick?: (value: number) => void
    onChangeText?: (text: string) => void
}

export const FeedbackCard = ({
    question1,
    question2,
    thisRating,
    showButtons,
    onClick,
    onChangeText
}: FeedbackCardProps) => {


    const handleClick = (val: number) => {
        onClick && onClick(val)
    }

    const handleChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
        onChangeText && onChangeText(event.target.value)
    }


    return (
        <div className={styles.card}>
            <p className={styles.firstQuestion}>{question1}</p>
            {
                showButtons &&
                <div className={styles.buttons}>
                    <IconButton
                        iconName='face4'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 1
                        })}  
                        onClick={() => handleClick(1)}
                    />
                    <IconButton
                        iconName='face3'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 2
                        })}  
                        onClick={() => handleClick(2)} 
                    />
                    <IconButton
                        iconName='face2'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 3
                        })}   
                        onClick={() => handleClick(3)}
                    />
                    <IconButton
                        iconName='face1'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 4
                        })}   
                        onClick={() => handleClick(4)}
                    />
                </div>
            }
            {question2 && <p className={styles.secondQusetion}>{question2}</p>} 
            <textarea
                className={styles.textarea}
                placeholder='Ваша відповідь...'
                onChange={handleChange}
            />
        </div>
    )
}
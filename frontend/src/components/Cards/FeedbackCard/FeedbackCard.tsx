import clsx from 'clsx'
import { IconButton } from '../../UI/IconButton/IconButton'
import styles from './FeedbackCard.module.scss'
import { ChangeEvent } from 'react'
import { useAppTranslator } from '../../../hooks/useAppTranslator'

interface FeedbackCardProps {
    tabIndex: number
    isError: boolean
    question1: string
    question2?: string
    showButtons?: boolean
    thisRating?: number
    onClick?: (value: number) => void
    onChangeText?: (text: string) => void
    onBlur?: (tabIndex: number) => void
}

export const FeedbackCard = ({
    tabIndex,
    isError,
    question1,
    question2,
    thisRating,
    showButtons,
    onClick,
    onChangeText,
    onBlur
}: FeedbackCardProps) => {

    const {t} = useAppTranslator()

    const handleClick = (val: number) => {
        onClick && onClick(val)
    }

    const handleChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
        onChangeText && onChangeText(event.target.value)
    }

    const handleBlur = () => {
        onBlur && onBlur(tabIndex)
    }

    return (
        <div 
            tabIndex={tabIndex}
            className={styles.card}
            onBlur={handleBlur}
        >
            <p className={styles.firstQuestion}>{question1}</p>
            {
                showButtons &&
                <div className={styles.buttons}>
                    <IconButton
                        type='button'
                        iconName='face4'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 1
                        })}  
                        onClick={() => handleClick(1)}
                    />
                    <IconButton
                        type='button'
                        iconName='face3'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 2
                        })}  
                        onClick={() => handleClick(2)} 
                    />
                    <IconButton
                         type='button'
                        iconName='face2'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 3
                        })}   
                        onClick={() => handleClick(3)}
                    />
                    <IconButton
                         type='button'
                        iconName='face1'
                        className={clsx(styles.button, {
                            [styles.active]: thisRating === 4
                        })}   
                        onClick={() => handleClick(4)}
                    />
                    { isError && <div className={styles.error_plug}>{t("change_rating")}</div>}
                </div>
            }
            {question2 && <p className={styles.secondQusetion}>{question2}</p>} 
            <textarea
                className={styles.textarea}
                placeholder={`${t('your_answer')}...`}
                onChange={handleChange}
            />
        </div>
    )
}
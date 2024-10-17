import { useNavigate } from 'react-router-dom'
import { Logo } from '../../components/Logo/Logo'
import { IconButton } from '../../components/UI/IconButton/IconButton'
import { useAppTranslator } from '../../hooks/useAppTranslator'
import styles from './InfoModal.module.scss'
import { useEffect } from 'react'
import { ROUTE } from '../../constants'

interface InfoModalProps {
    onClose: () => void
}

export const InfoModal = ({
    onClose
}: InfoModalProps) => {

    const {t} = useAppTranslator()

    const navigate = useNavigate()

    useEffect(() => {

        window.document.body.style.overflow = 'hidden'

        return () => {
            window.document.body.style.overflow = 'visible'
        }

    }, [])

    const move = () => {
        navigate(ROUTE.FEEDBACK)
        onClose()
    }

    return (
        <div 
            className={styles.container}
        >
            <div className={styles.modal}>
                <IconButton 
                    className={styles.button}
                    iconName='cross'
                    onClick={onClose}
                />
                <div className={styles.content}>
                    <header>{t('pay_attantion')}</header>
                    <div className={styles.info}>
                        <p>{t('training_project')}</p>
                        <p>{t('left_rewiew')} <button onClick={move}>{t('here')}</button></p> 
                    </div>
                    <Logo className={styles.logo}/>
                </div>
            </div>
        </div>
    )
}
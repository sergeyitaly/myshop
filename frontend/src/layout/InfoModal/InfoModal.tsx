import { Link } from 'react-router-dom'
import { Logo } from '../../components/Logo/Logo'
import { IconButton } from '../../components/UI/IconButton/IconButton'
import { useAppTranslator } from '../../hooks/useAppTranslator'
import styles from './InfoModal.module.scss'
import { useEffect } from 'react'

interface InfoModalProps {
    onClose: () => void
}

export const InfoModal = ({
    onClose
}: InfoModalProps) => {

    const {t} = useAppTranslator()

    useEffect(() => {

        window.document.body.style.overflow = 'hidden'

        return () => {
            window.document.body.style.overflow = 'visible'
        }

    }, [])

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
                    <p>{t('training_project')}</p>
                    <p>{t('left_rewiew')} <Link to={'https://docs.google.com/forms/d/e/1FAIpQLScXzBZeNqUsbB9iQYWlyCrdgrmUB0ZPOlVe_AhKwL9u1Nft0w/viewform'}>{t('here')}</Link></p> 
                    <Logo className={styles.logo}/>
                </div>
            </div>
        </div>
    )
}
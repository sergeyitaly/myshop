import { ReactNode, useEffect, useRef } from 'react'
import styles from './AppModal.module.scss'
import useClickOutside from '../../hooks/useClickOutside'

interface AppModalProps {
    children: ReactNode,
    open: boolean
    onClickOutside: () => void
}

export const AppModal = ({
    children,
    open,
    onClickOutside
}: AppModalProps) => {

    useEffect(() => {
        open ? 
            window.document.body.style.overflow = 'hidden' :
            window.document.body.style.overflow = 'visible'
    }, [open])

    const div = useRef(null)

    useClickOutside(div, onClickOutside)

    return (
        <>
        {
            open &&
            <div
                className={styles.modal}
            >
                <div 
                    className={styles.content}
                    ref = {div}
                >
                    {children}
                </div>
            </div>
        }
        </>
    )
}
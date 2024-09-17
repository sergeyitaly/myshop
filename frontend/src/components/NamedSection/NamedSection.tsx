import { DetailedHTMLProps } from "react"
import { PageContainer } from "../containers/PageContainer"
import styles from './NamedSection.module.scss'
import clsx from "clsx"
import { Skeleton } from "../Skeleton/Skeleton"

interface NamedSectionProps extends DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> {
    title: string 
    isLoading?: boolean
}

export const NamedSection = ({
    title,
    isLoading,
    ...props
}: NamedSectionProps) => {

    const { children } = props

    return (
        <section {...props}>
            <PageContainer>
                {
                    isLoading ? 
                        <Skeleton className={clsx(styles.title, styles.skeleton)}/>
                        :
                        <h1 className={styles.title}>{title}</h1>
                
                }
                {children}
            </PageContainer>
        </section>
    )
}

import {motion, Variants} from 'framer-motion'


interface MotionItemProps {
    children: JSX.Element
    delay?: number
    offset?: number
    index: number
}



export const MotionItem = ({
    children,
    delay = 0.15,
    offset = 200,
    index
}: MotionItemProps) => {

    const variants: Variants = {
        visible: (i: number)  => ({
            opacity: 1,
            y: 0,
            transition: {
            delay: i * delay,
            ease: 'linear'   
            },
             
        }),

        hidden: { opacity: 0, y: offset },
    }

    return (
        <motion.div
            custom={index}
            initial = 'hidden'
            animate = 'visible'
            variants={variants}
        >
            {children}
        </motion.div>
    )

}
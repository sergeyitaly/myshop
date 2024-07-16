
import {motion} from 'framer-motion'
import { ReactNode } from 'react'

interface MotionSearchProps {
    children: ReactNode
    className?: string
}

export const MotionSearch = ({
    children,
    className
}: MotionSearchProps) => {
    return (
        <motion.div 
        initial={{
            x: '-50%',
            top: '-100%',
            opacity: 0
        }}
        animate={{
            top: '100%',
            opacity: 1
        }}
        exit={{
            top: '-100%',
            opacity: 0
        }}
        className={className}
    >
        {children}
    </motion.div>
    )
}
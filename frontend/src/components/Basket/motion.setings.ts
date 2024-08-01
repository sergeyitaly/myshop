import { Variants } from "framer-motion";

export const modal: Variants = {
    hidden: {
        opacity: 0,
    },
    visible: {
        opacity: 1,
    }
}

export const box: Variants = {
    hidden: {
        x: '100%',
    },
    visible: {
        x: 0,
        transition: {
            when: 'beforeChildren',
            staggerChildren: .1,
            ease: 'linear',
            duration: .2
        }
        
    }
}

export const item: Variants = {
    hidden: {
        opacity: 0,
        x: -500
    },
    visible: {
        opacity: 1,
        x: 0,
        transition: {
            ease: 'linear'
        }
    }
}
import { Variants } from "framer-motion";

export const modal: Variants = {
    hidden: {
        opacity: 0,
        transition: {
            when: 'afterChildren'
        }
    },
    visible: {
        opacity: 1,
        transition: {
            when: 'beforeChildren',
        }
        
    }
}

export const box: Variants = {
    hidden: {
        x: '100%',
        transition: {
            when: 'afterChildren',
            staggerChildren: .1,
            duration: .2
        }
    },
    visible: {
        x: 0,
        transition: {
            when: 'beforeChildren',
            staggerChildren: .2,
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
import { SVGProps } from "react"

export const CrossSign = ({...props}: SVGProps<SVGSVGElement>) => {
    return (
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" strokeWidth='1.25' xmlns="http://www.w3.org/2000/svg" {...props}>
            <path d="M0.75 0.75L13.25 13.25M0.75 13.25L13.25 0.75" stroke="#0B0599" strokeWidth="inherit" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>

    )
}
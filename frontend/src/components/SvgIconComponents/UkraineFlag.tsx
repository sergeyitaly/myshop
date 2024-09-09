import { SVGProps } from "react"


export const UkraineFlagIcon = ({
    ...props
}: SVGProps<SVGSVGElement>) => {

    return (
        <svg width="513" height="512" viewBox="0 0 513 512" fill="none" xmlns="http://www.w3.org/2000/svg" {...props}>
        <g clip-path="url(#clip0_103_67)">
        <path fillRule="evenodd" clipRule="evenodd" d="M0.5 0H512.5V512H0.5V0Z" fill="#FFD700"/>
        <path fillRule="evenodd" clipRule="evenodd" d="M0.5 0H512.5V256H0.5V0Z" fill="#0057B8"/>
        </g>
        <defs>
        <clipPath id="clip0_103_67">
        <rect width="512" height="512" fill="white" transform="translate(0.5)"/>
        </clipPath>
        </defs>
        </svg>



    )
}

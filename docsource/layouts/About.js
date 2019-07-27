// Components
import Boot            from '../components/Boot';
import Navbar          from '../components/Navbar';
import SideNav         from '../components/SideNav';
import Footer          from '../components/Footer';
import SearchResults   from '../components/SearchResults';
import EjrbussMarkdown from '../components/EjrbussMarkdown';
import Places          from '../components/Places';
import Profile         from '../components/Profile';

// Libraries
import Pages from '../lib/Pages';
import Vars  from '../Vars';
import { useSearch } from '../lib/hooks';

export default ({ pageName }) => {
    const page      = Pages[pageName];
    const searchCtx = useSearch();
    return (
        <>
            <div id='page'>
            <Boot { ...page } />
                <Navbar
                    searchCtx={searchCtx}
                    showScrollMarker
                    showSearch
                    leftLinks={<Places {...{ [page.place]: true }} />}
                    rightLinks={<a target='_blank' href={Vars.github} className='p-md subtle-accent'>
                        <i className='fab fa-github fa-lg' />
                    </a>}
                />
                <SideNav />
                <SearchResults searchCtx={searchCtx} />
                <div className='content container grid-md'>
                    <EjrbussMarkdown source=
{`
# Meet Our Team

We are a group of Software and Electrical Engineering students from the University of Victoria. We combined our passions for programming, artificial intelligence, and gaming to deliver an artificial intelligence tool to help newcomers discover a love for technology and creating something new.
`}
                    />
                    <Profile src='../static/img/Eric.png' name='Eric Buss' position='Team Lead / Developer'>
                        <EjrbussMarkdown
                            source=
{`
Eric is a fourth-year Software Engineering student graduating in August 2019. He is a Canadian through-and-through having already lived and worked in 5 Canadian provinces. His love for creative projects and problem-solving led him to his studies at UVic. Eric brings his passion for code and design to all his projects both in and out of school.`}
                        />
                        <a href='https://www.linkedin.com/in/ejrbuss/' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='https://github.com/ejrbuss' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/Torrey.png' right name='Torrey Randolph' position='Low Level Architect'>
                        <EjrbussMarkdown
                            source=
{`
Torrey plans to graduate from UVic with a Bachelor of Software Engineering in 2019. Come October, she will be starting her career as a Firmware Developer at Reliable Controls in the beautiful city of Victoria. She hopes to one day follow her dream of working for NASA.`}
                        />
                        <a href='https://www.linkedin.com/in/torrey-randolph/' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='https://github.com/torreyr' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/Jon.png' name='Jonathan Bezeau' position='Artist / Developer'>
                        <EjrbussMarkdown
                            source=
{`
Jon is a fourth year Software Engineering student aiming to graduate in 2020. He hails from Prince George BC, and moved to Victoria to study general engineering at UVic in 2014. Jon spends his time writing Dungeons and Dragons campaigns and working on his personal coding projects. After graduation he hopes to remain in Victoria.`}
                        />
                        {/* <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a> */}
                        <a href='https://github.com/UltravioletVoodoo' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/James.png' right name='James Barlow' position='UI Developer'>
                        <EjrbussMarkdown
                            source=
{`
James is graduating from UVic with a Software Engineering degree and Business minor in August 2019. He wants to try his hand at running a business someday, but until then he hopes to work on technologies that help people. Further education is still a possibility for the future, but right now he is excited to start his career.
`}
                        />
                        {/* <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a> */}
                        <a href='https://github.com/jbarlo' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/Andrew.png' name='Andrew Wiggins' position='Web Developer'>
                        <EjrbussMarkdown
                            source=
{`
Andrew is a fourth year Software Engineering student who plans on graduating in April 2020. He started his University career in the Faculty of Science, but transitioned into Software Engineering after discovering a fondness for programming. After graduation he plans on moving to Vancouver to pursue a career as a developer.
`}
                        />
                        <a href='https://www.linkedin.com/in/awiggs96/' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='https://www.github.com/awiggs' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/John.png' right name='Forrest Curry' position='AI Developer'>
                        <EjrbussMarkdown
                            source=
{`
Forrest is a fourth year Bachelor of Electrical Engineering student with a Minor in Computer Science. He has experience working both high level technologies such as web development and low level technologies such as integrated circuit design as well as software designed to target embedded systems. As for computer support, he has worked as an IT profession for both desktop and remote system administration. Personally, he loves a good sci-fi book and has been playing guitar since he was 17.`}
                        />
                        <a href='https://www.linkedin.com/in/john-curry/' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='https://github.com/john-curry' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <br/>
                    <EjrbussMarkdown source=
{`
# Acknowledgements
Chip-Gr8 would not have been possible without the help of several individuals. We would like to acknowledge their involvement in Chip-Gr8's development journey, and extend to them our deepest thanks.

## Faculty Supervisor
`}
                    />
                    <Profile src='../static/img/red.png' name='Rich Little' position='Faculty Supervisor'>
                        <EjrbussMarkdown
                            source=
{`
We chose Rich Little as our faculty supervisor for his background in algorithms and based on our positive experiences with him in CSC 225 and 226 courses. He was responsible for supervising the project during its development cycle and for marking all of the milestones. Thank you to Rich Little for the help he provided along the way.
`}
                        />
                    </Profile>
                    <br/>
                    <EjrbussMarkdown source=
{`
## Supporters

Thank you to Dr. Xiaodai Dong for being the primary instructor this semester.

Thank you to Dr. Ilamparithi for being the course coordinator this semester.

Thank you to Sai Prakash Reddy Konda, our TA, for their help with the course.
`}
                    />
                </div>
            </div>
            <Footer />
        </>
    );
};
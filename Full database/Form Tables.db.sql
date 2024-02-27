BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS users (
    u_lastname  varchar(255) not null,
    u_firstname       varchar(255) not null,
    u_depname  varchar(255) not null,
    u_job     varchar(255) not null,
    u_email        varchar(255) not null,
)
CREATE TABLE IF NOT EXISTS education (
    e_schoolname     decimal(8,0) not null,
    e_location        varchar(55) not null,
    e_degree     varchar(55) not null,
    e_program      varchar(55) not null
    e_gradyear      varchar(55) not null
);
CREATE TABLE IF NOT EXISTS profHistory (
    p_employer     varchar(55) not null,
    p_title    varchar(55) not null,
    p_startYear   varchar(55) not null,
    p_endyear    varchar(55) not null,
    p_function  varchar(55) not null
    p_responsibility  varchar(55) not null
)
CREATE TABLE IF NOT EXISTS type (
    t_type varchar(55) not null,
)
CREATE TABLE IF NOT EXISTS individual (
    i_impact       varchar(152) not null,
    i_patent       decimal(9,0) not null
    i_performance       decimal(9,0) not null
    i_responsibility       decimal(9,0) not null
    i_future       decimal(9,0) not null
)

CREATE TABLE IF NOT EXISTS project (
    pr_impact       varchar(152) not null,
    pr_contributions       decimal(9,0) not null
    pr_compare       decimal(9,0) not null
    pr_responsibility       decimal(9,0) not null
    pr_future       decimal(9,0) not null
)
CREATE TABLE IF NOT EXISTS people (
    pe_impact       varchar(152) not null,
    pe_contributions       decimal(9,0) not null
    pe_compare       decimal(9,0) not null
    pe_responsibility       decimal(9,0) not null
    pe_future       decimal(9,0) not null
)
CREATE TABLE IF NOT EXISTS awards (
    a_awards    varchar(55) not null
)
CREATE TABLE IF NOT EXISTS activities (
    ac_activities    varchar(55) not null
)
CREATE TABLE IF NOT EXISTS recommendations (
    r_recommendations    varchar(55) not null
)

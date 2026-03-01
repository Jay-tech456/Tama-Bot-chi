import {defineField, defineType} from 'sanity'

export const userProfileType = defineType({
  name: 'userProfile',
  title: 'User Profile',
  type: 'document',
  fields: [
    defineField({
      name: 'userId',
      title: 'User ID',
      type: 'string',
      validation: (rule) => rule.required(),
      description: 'Unique identifier for the user',
    }),
    defineField({
      name: 'name',
      title: 'Name',
      type: 'string',
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: 'email',
      title: 'Email',
      type: 'string',
      validation: (rule) => rule.required().email(),
    }),
    defineField({
      name: 'phone',
      title: 'Phone Number',
      type: 'string',
    }),
    defineField({
      name: 'interests',
      title: 'Interests',
      type: 'array',
      of: [{type: 'string'}],
      description: 'User interests for matching (e.g., AI, startups, design)',
    }),
    defineField({
      name: 'industry',
      title: 'Industry',
      type: 'string',
      description: 'Primary industry (e.g., Technology, Healthcare, Finance)',
    }),
    defineField({
      name: 'role',
      title: 'Role/Title',
      type: 'string',
      description: 'Current job role or title',
    }),
    defineField({
      name: 'seniority',
      title: 'Seniority Level',
      type: 'string',
      options: {
        list: [
          {title: 'Student/Entry Level', value: 'entry'},
          {title: 'Mid-level', value: 'mid'},
          {title: 'Senior', value: 'senior'},
          {title: 'Lead/Principal', value: 'lead'},
          {title: 'Executive/C-Level', value: 'executive'},
        ],
      },
    }),
    defineField({
      name: 'goals',
      title: 'Goals',
      type: 'array',
      of: [{type: 'string'}],
      description: 'Professional goals (e.g., raise funding, hire engineers, learn about AI)',
    }),
    defineField({
      name: 'bio',
      title: 'Bio',
      type: 'text',
      rows: 4,
      description: 'Short biography or professional summary',
    }),
    defineField({
      name: 'location',
      title: 'Location',
      type: 'string',
      description: 'City or region',
    }),
    defineField({
      name: 'linkedinUrl',
      title: 'LinkedIn URL',
      type: 'url',
    }),
    defineField({
      name: 'twitterHandle',
      title: 'Twitter/X Handle',
      type: 'string',
      description: 'Twitter/X username (without @)',
    }),
    defineField({
      name: 'availability',
      title: 'Availability',
      type: 'object',
      fields: [
        {
          name: 'status',
          title: 'Status',
          type: 'string',
          options: {
            list: [
              {title: 'Available', value: 'available'},
              {title: 'Limited', value: 'limited'},
              {title: 'Unavailable', value: 'unavailable'},
            ],
          },
        },
        {
          name: 'note',
          title: 'Note',
          type: 'string',
          description: 'Optional availability note',
        },
      ],
    }),
  ],
  preview: {
    select: {
      title: 'name',
      subtitle: 'role',
      media: 'image',
    },
  },
})
